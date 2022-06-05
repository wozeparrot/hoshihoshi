const { Live2DModel, ZipLoader } = PIXI.live2d;

// register zip loading
ZipLoader.zipReader = (data, url) => JSZip.loadAsync(data);
ZipLoader.readText = (reader, path) => {
    const file = reader.file(path);
    return file.async('text');
}
ZipLoader.getFilePaths = (reader) => {
    const paths = [];
    reader.forEach((relPath) => paths.push(relPath));
    return Promise.resolve(paths);
}
ZipLoader.getFiles = (reader, paths) =>
    Promise.all(paths.map(async path => {
        const name = path.slice(path.lastIndexOf("/") + 1);
        const blob = await reader.file(path).async('blob');
        return new File([blob], name);
    }));

document.getElementById("zippicker").addEventListener("change", async (event) => {
    const files = event.target.files;
    if (!files.length) return;

    // hide picker
    document.getElementById("zp_container").style.display = "none";

    // create pixi application
    const app = new PIXI.Application({
        view: document.getElementById("live2d"),
        autoStart: true,
        backgroundAlpha: 0,
        backgroundColor: 0x00ff00,
        resizeTo: window,
    });

    // load model
    const model = await Live2DModel.from([files[0]], { autoInteract: false });
    const core = model.internalModel.coreModel;
    model.anchor.set(0.5, 0.5);
    model.centerOffsetX = 1920/2;
    model.centerOffsetY = 1080/2;
    model.scaleOffset = 0.5;
    model.interactive = true;

    // render to rendertexture and sprite
    const renderTexture = new PIXI.RenderTexture(new PIXI.BaseRenderTexture(app.screen.width, app.screen.height));
    const sprite = new PIXI.Sprite(renderTexture);
    document.querySelector("#live2d").addEventListener("pointerdown", e => {
        model.offsetX = e.x - model.centerOffsetX;
        model.offsetY = e.y - model.centerOffsetY;
        model.dragging = true;
    });
    document.querySelector("#live2d").addEventListener("pointerup", () => {
        model.dragging = false;
    });
    document.querySelector("#live2d").addEventListener("pointermove", e => {
        if (model.dragging) {
            model.centerOffsetX = e.x - model.offsetX;
            model.centerOffsetY = e.y - model.offsetY;
        }
    });
    document.querySelector("#live2d").addEventListener("wheel", e => {
        e.preventDefault();
        model.scaleOffset = model.scaleOffset - e.deltaY * -0.0001;
    });

    // render every tick
    app.ticker.add(() => {
        app.renderer.render(model, renderTexture);
    });
    app.stage.addChild(sprite);

    // receive tracking data from websocket
    const ws = new WebSocket("ws://" + window.location.hostname + ":6789");
    ws.onmessage = ({ data }) => {
        const result = JSON.parse(data);

        const scaled_translation_x = result.head_translation.x * 10;
        const scaled_translation_y = result.head_translation.y * 10;
        model.position.set(
            scaled_translation_x + model.centerOffsetX,
            scaled_translation_y + model.centerOffsetY,
        );
        const scaled_translation_z = 1.5 - Math.min(Math.max(result.head_translation.z / 60, 0.0), 1.5 - 0.1);
        model.scale.set(
            scaled_translation_z - model.scaleOffset
        );

        model.internalModel.motionManager.update = () => {
            model.internalModel.eyeBlink = undefined;

            core.setParamFloat(
                "PARAM_ANGLE_X",
                result.head_rotation.y,
            );
            core.setParamFloat(
                "PARAM_ANGLE_Y",
                -result.head_rotation.x + 180,
            );
            core.setParamFloat(
                "PARAM_ANGLE_Z",
                -result.head_rotation.z,
            );

            core.setParamFloat(
                "PARAM_BODY_ANGLE_X",
                result.head_rotation.y * 0.3,
            );
            core.setParamFloat(
                "PARAM_BODY_ANGLE_Y",
                (-result.head_rotation.x + 180) * 0.3,
            );
            core.setParamFloat(
                "PARAM_BODY_ANGLE_Z",
                -result.head_rotation.z * 0.3,
            );

            core.setParamFloat(
                "PARAM_EYE_BALL_X",
                result.iris.x
            );
            core.setParamFloat(
                "PARAM_EYE_BALL_Y",
                result.iris.y - 0.5
            );

            core.setParamFloat(
                "PARAM_MOUTH_OPEN_Y",
                result.mouth.y,
            );
            core.setParamFloat(
                "PARAM_MOUTH_FORM",
                result.mouth.x,
            );

            core.setParamFloat("PARAM_EYE_L_OPEN", result.eye.left);
            core.setParamFloat("PARAM_EYE_R_OPEN", result.eye.right);

            return true;
        };
    };
});

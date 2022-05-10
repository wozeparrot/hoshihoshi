const { Live2DModel } = PIXI.live2d;

(async function main() {
    // create pixi application
    const app = new PIXI.Application({
        view: document.getElementById("live2d"),
        autoStart: true,
        backgroundAlpha: 0,
        backgroundColor: 0x00ff00,
        width: 1280,
        height: 720,
    });

    // load model
    const model = await Live2DModel.from("https://iseng-domathid.vercel.app/rem/model.json", { autoInteract: false });
    const motion = model.internalModel.motionManager;
    const core = model.internalModel.coreModel;
    model.anchor.set(0.5, 0.5);
    model.position.set(app.screen.width / 2, app.screen.height / 1.5);
    model.scale.set(0.4);
    model.interactive = true;

    // render to rendertexture and sprite
    const renderTexture = new PIXI.RenderTexture(new PIXI.BaseRenderTexture(app.screen.width, app.screen.height));
    const sprite = new PIXI.Sprite(renderTexture);
    document.querySelector("#live2d").addEventListener("pointerdown", e => {
        model.offsetX = e.x - model.position.x;
        model.offsetY = e.y - model.position.y;
        model.dragging = true;
    });
    document.querySelector("#live2d").addEventListener("pointerup", e => {
        model.dragging = false;
    });
    document.querySelector("#live2d").addEventListener("pointermove", e => {
        if (model.dragging) {
            model.position.set(
                e.x - model.offsetX,
                e.y - model.offsetY
            );
        }
    });
    document.querySelector("#live2d").addEventListener("wheel", e => {
        e.preventDefault();
        model.scale.set(
            model.scale.x + e.deltaY * -0.0001
        );
    });

    // render every tick
    app.ticker.add(() => {
        app.renderer.render(model, renderTexture);
    });
    app.stage.addChild(sprite);

    // receive tracking data from websocket
    const ws = new WebSocket("ws://127.0.0.1:6789");
    ws.onmessage = ({ data }) => {
        const result = JSON.parse(data);

        model.internalModel.motionManager.update = (...args) => {
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
                "PARAM_MOUTH_FROM",
                result.mouth.x,
            );

            core.setParamFloat("PARAM_EYE_L_OPEN", result.eye.left);
            core.setParamFloat("PARAM_EYE_R_OPEN", result.eye.right);

            return true;
        };

        // ws.send(app.renderer.plugins.extract.base64(renderTexture));
    };
})();

const { Application } = PIXI;
const { Live2DModel } = PIXI.live2d;

(async function main() {
    // create pixi application
    const app = new PIXI.Application({
        view: document.getElementById("live2d"),
        autoStart: true,
        backgroundAlpha: 0,
        backgroundColor: 0x00ff00,
        resizeTo: window
    });

    // load model
    const model = await Live2DModel.from("https://iseng-domathid.vercel.app/rem/model.json", { autoInteract: false });
    const motion = model.internalModel.motionManager;
    const core = model.internalModel.coreModel;
    model.scale.set(0.4);
    model.interactive = true;
    model.anchor.set(0.5, 0.5);
    model.position.set(window.innerWidth * 0.5, window.innerHeight * 0.8);
    model.on("pointerdown", e => {
        model.offsetX = e.data.global.x - model.position.x;
        model.offsetY = e.data.global.y - model.position.y;
        model.dragging = true;
    });
    model.on("pointerup", e => {
        model.dragging = false;
    });
    model.on("pointermove", e => {
        if (model.dragging) {
            model.position.set(
                e.data.global.x - model.offsetX,
                e.data.global.y - model.offsetY
            );
        }
    });
    document.querySelector("#live2d").addEventListener("wheel", e => {
        e.preventDefault();
        model.scale.set(
            model.scale.x + e.deltaY * -0.0001
        );
    });
    app.stage.addChild(model);

    // connect to websocket
    const ws = new WebSocket("ws://10.11.235.99:6789");
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
                result.iris.y
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
    };


})();

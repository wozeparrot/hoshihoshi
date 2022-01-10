const ws = new WebSocket("ws://10.11.235.99:6789");
ws.onmessage = ({ data }) => {
    document.getElementById("render").src = data;
};
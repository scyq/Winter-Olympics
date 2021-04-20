import { action, makeObservable, observable } from "mobx";
const host = "http://127.0.0.1:8000";

class Store {

    constructor() {
        makeObservable(this);
    }

    @observable signalPath = [undefined, undefined, undefined, undefined];
    @observable playground = require("./assets/playground.jpg").default;

    /**
     * 
     * @param {number} signalIndex 1，2，3，4
     * @param {string} path 路径
     */
    @action
    changeSignalPath(signalIndex, path) {
        this.signalPath[signalIndex - 1] = path;
    }

    @action
    loadSignal() {
        for (let i = 0; i < this.signalPath.length; i++)
            this.signalPath[i] = require("./assets/example.mp4").default;
    }

    vr() {
        fetch(host + "/vr")
            .then(res => res.json())
            .then(data => console.log(data));
    }

    start() {
        fetch(host + "/start")
            .then(res => res.body)
            .then(body => {
                const reader = body.getReader();
                return new ReadableStream({
                    start(controller) {
                        return pump();
                        function pump() {
                            return reader.read().then(({ done, value }) => {
                                if (done) {
                                    controller.close();
                                    return;
                                }
                                controller.enqueue(value);
                                return pump();
                            });
                        }
                    }
                });
            })
            .then(stream => new Response(stream))
            .then(response => response.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(url => this.playground = url)

    }

    @action
    analysisDone() {
        console.log(1)
        try {
            this.playground = require("./assets/frame.jpg").default;
        } finally {

        }
    }
}

export default new Store();
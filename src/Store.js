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

    start() {
        fetch(host + "/start")
            .then(res => res.json())
            .then(data => {
                if (data) {
                    this.analysisDone();
                }
            });
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
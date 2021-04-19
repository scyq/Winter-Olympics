import { action, makeObservable, observable } from "mobx";

class Store {

    constructor() {
        makeObservable(this);
    }

    @observable signalPath = [undefined, undefined, undefined, undefined];

    /**
     * 
     * @param {number} signalIndex 1，2，3，4
     * @param {string} path 路径
     */
    @action
    changeSignalPath(signalIndex, path) {
        this.signalPath[signalIndex - 1] = path;
    }
}

export default new Store();
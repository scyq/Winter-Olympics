import { makeObservable, observable } from "mobx";

class Store {

    constructor() {
        makeObservable(this);
    }

    @observable signalPath1 = undefined;
    @observable signalPath2 = undefined;
    @observable signalPath3 = undefined;
    @observable signalPath4 = undefined;

}

export default new Store();
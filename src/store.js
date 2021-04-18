import { action, makeObservable, observable } from "mobx";

class Store {
    constructor() {
        makeObservable(this);
    }
}
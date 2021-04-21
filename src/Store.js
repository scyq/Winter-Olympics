import { action, makeObservable, observable } from "mobx";
const host = "http://127.0.0.1:8000";

class Store {

    constructor() {
        makeObservable(this);
    }

    @observable signalPath = [undefined, undefined, undefined, undefined];
    @observable playground = require("./assets/playground.jpg").default;
    @observable playgroundHeight = 800;
    @observable reportOpen = false;
    @observable report = ["准备就绪"];


    @observable coordinates = [];
    @observable coordinatesLine = 0;

    @action
    loadSignal() {
        this.signalPath[0] = require("./assets/1.mp4").default;
        this.signalPath[1] = require("./assets/2.mp4").default;
        this.signalPath[2] = require("./assets/3.mp4").default;
        this.signalPath[3] = require("./assets/4.mp4").default;
        this.report = this.report.concat(["视频加载完成"]);
    }

    vr() {
        fetch(host + "/vr")
            .then(res => res.json())
            .then(data => console.log(data))
            .then(this.changeReport("虚拟现实系统已启动"));
    }

    @action
    showResult() {
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
    changeReport(append) {
        this.report = this.report.concat([append]);
    }

    @action
    start() {
        if (!this.signalPath[0] && !this.signalPath[1] && !this.signalPath[2] && !this.signalPath[3]) {
            this.changeReport("请先输入视频信号！");
        } else {
            let startTime = new Date().getTime()
            fetch(host + "/fetch_coordinates")
                .then(res => res.json())
                .then(data => this.coordinates = data)
                .then(() => {
                    this.changeReport("冰壶检测开始");
                })
                .then(() => {
                    let interval = setInterval(() => {
                        let readTime = 5;
                        while (readTime > 0) {
                            this.changeReport([this.coordinates[this.coordinatesLine].join(" ")]);
                            this.coordinatesLine++;
                            readTime--;
                        }
                        let current = new Date().getTime();
                        if (current - startTime > 6000) {
                            clearInterval(interval);
                            this.showResult();
                            if (this.coordinatesLine > 300) {
                                this.coordinatesLine = 0;
                            }
                            this.changeReport("检测完毕，已更新轨迹图");
                        }
                    }, 1000);
                });
        }
    }

    @action
    analysisDone() {
        try {
            this.playground = require("./assets/frame.jpg").default;
        } finally {

        }
    }

    @action
    triggerReport() {
        this.reportOpen = !this.reportOpen;
    }

    @action
    handleScroll(e) {
        console.log(e);
        e.preventDefault();
        this.playgroundHeight -= e.deltaY;
    }
}

export default new Store();
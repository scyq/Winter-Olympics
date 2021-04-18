import { Button, Upload } from "antd";
import { inject, observer } from "mobx-react";
import React from "react";
import Player from "../Player/Player"
import "./Cameras.css";

@inject("store")
@observer
class Cameras extends React.Component {
    render() {

        const { store } = this.props;

        return (
            <div className="Cameras">

                <div className="one-row">
                    <div className="signal-video">
                        <div>信号源1</div>
                        <Player></Player>
                    </div>

                    <div className="signal-video">
                        <div>信号源2</div>
                        <Player></Player>
                    </div>
                </div>

                <div className="one-row">
                    <div className="signal-video">
                        <div>信号源3</div>
                        <Player></Player>
                    </div>

                    <div className="signal-video">
                        <div>信号源4</div>
                        <Player></Player>
                    </div>
                </div>

                <div className="config">
                    <div className="signal-input">
                        <div className="title">信号源1</div>
                        <div className="path">{store.signalPath1 ? store.signalPath1 : "请正确选择信号源"}</div>
                        <Upload>
                            <Button>...</Button>
                        </Upload>
                    </div>

                    <div className="signal-input">
                        <div className="title">信号源2</div>
                        <div className="path">{store.signalPath2 ? store.signalPath2 : "请正确选择信号源"}</div>
                        <Upload>
                            <Button>...</Button>
                        </Upload>
                    </div>

                    <div className="signal-input">
                        <div className="title">信号源3</div>
                        <div className="path">{store.signalPath3 ? store.signalPath3 : "请正确选择信号源"}</div>
                        <Upload>
                            <Button>...</Button>
                        </Upload>
                    </div>

                    <div className="signal-input">
                        <div className="title">信号源4</div>
                        <div className="path">{store.signalPath4 ? store.signalPath4 : "请正确选择信号源"}</div>
                        <Upload>
                            <Button>...</Button>
                        </Upload>
                    </div>
                </div>
            </div>
        );
    }
}

export default Cameras;
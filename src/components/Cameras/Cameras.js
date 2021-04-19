import { inject, observer } from "mobx-react";
import React from "react";
import Player from "../Player/Player"
import "./Cameras.css";

@inject("store")
@observer
class Cameras extends React.Component {

    /**
     * @param {ChangeEvent<HTMLInputElement>} e file selection
     */
    videoSelection(e, idx, store) {
        const [file] = e.target.files;
        store.changeSignalPath(idx, URL.createObjectURL(file));
    }

    render() {
        const { store } = this.props;

        return (
            <div className="Cameras">

                <div className="one-row">
                    <div className="signal-video">
                        <div>信号源1</div>
                        <Player path={store.signalPath[0]}></Player>
                    </div>

                    <div className="signal-video">
                        <div>信号源2</div>
                        <Player path={store.signalPath[1]}></Player>
                    </div>
                </div>

                <div className="one-row">
                    <div className="signal-video">
                        <div>信号源3</div>
                        <Player path={store.signalPath[2]}></Player>
                    </div>

                    <div className="signal-video">
                        <div>信号源4</div>
                        <Player path={store.signalPath[3]}></Player>
                    </div>
                </div>
            </div>
        );
    }
}

export default Cameras;
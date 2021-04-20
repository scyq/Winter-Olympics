import React from "react";
import "./Controller.css";
import { inject, observer } from "mobx-react";
import Button from '@material-ui/core/Button';
import VideocamSharpIcon from '@material-ui/icons/VideocamSharp';
import PlayCircleOutlineSharpIcon from '@material-ui/icons/PlayCircleOutlineSharp';
import ThreeDRotationSharpIcon from '@material-ui/icons/ThreeDRotationSharp';
import StorageSharpIcon from '@material-ui/icons/StorageSharp';

@inject("store")
@observer
class Controller extends React.Component {
    render() {
        const { store } = this.props;
        return (
            <div className="Controller">
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<VideocamSharpIcon />}
                    onClick={() => { store.loadSignal(); }}>
                    输入视频
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<PlayCircleOutlineSharpIcon />}
                    onClick={() => { store.start(); }}>
                    轨迹生成
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<ThreeDRotationSharpIcon />}
                    onClick={() => { store.vr(); }} >
                    虚拟现实
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<StorageSharpIcon />}
                    onClick={() => { store.triggerReport(); }} >
                    结果显示
                </Button>
            </div >
        );
    }
}

export default Controller;
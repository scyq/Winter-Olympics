import { Button } from "antd";
import React from "react";
import "./Controller.css";
import { PlayCircleFilled, CodepenOutlined, ApiFilled } from '@ant-design/icons';
import { inject, observer } from "mobx-react";

@inject("store")
@observer
class Controller extends React.Component {
    render() {
        const { store } = this.props;
        return (
            <div className="Controller">
                <Button id="loadSignal" icon={<ApiFilled />} onClick={() => { store.loadSignal() }}>输入视频</Button>
                <Button id="startBtn" icon={<PlayCircleFilled />} onClick={() => { store.start() }}>轨迹生成</Button>
                <Button id="vrBtn" icon={<CodepenOutlined />} onClick={() => { store.vr() }} >虚拟现实</Button>
                <Button id="dataBtn" icon={<CodepenOutlined />} onClick={() => { store.vr() }} >过程显示</Button>
            </div>
        );
    }
}

export default Controller;
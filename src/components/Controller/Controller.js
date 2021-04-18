import { Button } from "antd";
import React from "react";
import "./Controller.css";
import { PlayCircleFilled, CodepenOutlined } from '@ant-design/icons';

class Controller extends React.Component {
    render() {
        return (
            <div className="Controller">
                <Button id="startBtn" icon={<PlayCircleFilled />}>开始评估</Button>
                <Button id="vrBtn" icon={<CodepenOutlined />} >虚拟现实</Button>
            </div>
        );
    }
}

export default Controller;
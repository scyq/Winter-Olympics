import React from "react";
import './Player.css';

class Player extends React.Component {
    render() {
        return (
            <video className="Player" src={this.props.path} controls height="300px" autoPlay></video>
        );
    }
}


export default Player;
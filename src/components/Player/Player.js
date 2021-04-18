import React from "react";
import './Player.css';
import mp4 from "../../assets/example.mp4"


class Player extends React.Component {
    render() {
        return (
            <video className="Player" controls height="300">
                <source src={mp4}
                    type="video/mp4"></source>
            </video>
        );
    }
}


export default Player;
import './App.css';
import React from 'react';
import Cameras from './components/Cameras/Cameras';
import { Provider } from 'mobx-react';
import playground from "./assets/playground.jpg";
import Controller from './components/Controller/Controller';

class App extends React.Component {

  render() {
    return (
      <Provider {...this.props}>
        <div className="App">
          <div className="Controller">
            <Controller></Controller>
          </div>
          <div className="playground">
            <img src={playground} alt="playground" style={{ height: "1200px" }}></img>
          </div>
          <Cameras></Cameras>
        </div>
      </Provider>
    );
  }
}
export default App;

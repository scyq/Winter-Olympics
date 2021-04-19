import './App.css';
import React from 'react';
import Cameras from './components/Cameras/Cameras';
import { inject, observer, Provider } from 'mobx-react';
import Controller from './components/Controller/Controller';

@inject("store")
@observer
class App extends React.Component {

  render() {

    const { store } = this.props;

    return (
      <Provider {...this.props}>
        <div className="App">
          <div className="Controller">
            <Controller></Controller>
          </div>
          <div className="playground">
            <img src={store.playground} alt="playground" style={{ height: "1200px" }}></img>
          </div>
          <Cameras></Cameras>
        </div>
      </Provider>
    );
  }
}
export default App;

import './App.css';
import React from 'react';
import Cameras from './components/Cameras/Cameras';
import { inject, observer, Provider } from 'mobx-react';
import Controller from './components/Controller/Controller';
import Header from './components/Header/Header';

@inject("store")
@observer
class App extends React.Component {

  render() {

    const { store } = this.props;

    return (
      <Provider {...this.props}>
        <div className="App">
          <Header></Header>
          <div className="row-panel">
            <Controller></Controller>
            <Cameras></Cameras>
          </div>
          <div className="playground">
            <img src={store.playground} alt="playground" style={{ width: "80%" }}></img>
          </div>
        </div>
      </Provider>
    );
  }
}
export default App;

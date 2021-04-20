import './App.css';
import React from 'react';
import Cameras from './components/Cameras/Cameras';
import { inject, observer, Provider } from 'mobx-react';
import Controller from './components/Controller/Controller';
import Header from './components/Header/Header';
import Process from './components/Process/Process';

@inject("store")
@observer
class App extends React.Component {

  render() {
    const { store } = this.props;

    return (
      <Provider {...this.props}>
        <Process open={store.reportOpen} trigger={() => store.triggerReport()} report={store.report}></Process>
        <div className="App">
          <div>
            <Header></Header>
            <div className="row-panel">
              <div className="playground-div" onWheel={e => store.handleScroll(e)}>
                <img className="playground" src={store.playground} alt="playground" style={{ height: store.playgroundHeight + "px" }}></img>
              </div>
              <div className="col-panel">
                <Controller></Controller>
                <Cameras></Cameras>
              </div>
            </div>
          </div>
        </div>
      </Provider >
    );
  }
}
export default App;

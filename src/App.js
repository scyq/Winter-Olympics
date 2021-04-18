import './App.css';
import React from 'react';
import Cameras from './components/Cameras/Cameras';

class App extends React.Component {

  render() {
    return (
      <div className="App">
        <Cameras></Cameras>
      </div>
    );
  }
}
export default App;

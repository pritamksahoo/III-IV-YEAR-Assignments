import React, {Component} from 'react';
import mainClasses from './App.module.css';
import {Screen} from './screen/screen';
import {Keypad} from './keypad/keypad';

class App extends Component {
  	state = {
		screenString: "0"
  	}

  	render = () => {
    	return (
      		<div className={mainClasses.Calculator}>
        		<Screen screenString={this.state.screenString} />
				<Keypad />
      		</div>
    	)
  	}
}

export default App;

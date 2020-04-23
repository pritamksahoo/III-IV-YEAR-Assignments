import React, {Component} from 'react';
import mainClasses from './App.module.css';
import {Screen} from './screen/screen';
import {Keypad} from './keypad/keypad';
import {digit} from './keypad/digit';
import './keypad/keypad.css';

class App extends Component {
  	state = {
		screenString: "0"
  	}

	onKeyPadClick = (id, classname, icon) => {
		let allClasses = classname.split(' ')

		if (allClasses.indexOf("digit") >= 0) {
			// console.log("true")
			if (allClasses.indexOf("decimal") >= 0) {

			} else {
				this.setState((prevState, prevProps) => {
					return {screenString: prevState.screenString === "0" ? icon : prevState.screenString + icon}
				})
			}
		}
	}

	digitDiv = digit.map((item) => {
        return (
			<Keypad id={item.id} key={item.id} class={item.class} icon={item.icon} onclick={() => {return this.onKeyPadClick(item.id, item.class, item.icon)} } />
        )
    })

	// shouldComponentUpdate() {
	// 	console.log("hello")
	// 	return true
	// }

  	render = () => {
    	return (
      		<div className={mainClasses.Calculator}>
        		<Screen screenString={this.state.screenString} />
				
				<div className="Keypad">
                	{this.digitDiv}
            	</div>
      		</div>
    	)
  	}
}

export default App;

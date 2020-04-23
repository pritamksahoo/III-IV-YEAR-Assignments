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
		// console.log("hello")
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

	onKeyUp = (e) => {
		// console.log("default")
		e.preventDefault()
		let kc = e.keyCode

		let key = digit.filter((item, pos) => {
			if (item.keyCode === kc) {
				return true
			} else {
				return false
			}
		})
		// console.log(key)
		if (key.length === 0) {

		} else {
			let keyItem = key[0]

			let color = getComputedStyle(document.getElementById(keyItem.id)).backgroundColor

			if (keyItem.class.split(' ').indexOf("digit") >= 0) {
				document.getElementById(keyItem.id).style.backgroundColor = 'rgb(230, 230, 230)'
			} else {
				document.getElementById(keyItem.id).style.backgroundColor = 'rgb(192, 192, 192)'
			}
			// console.log(color)
			setTimeout(() => {
				document.getElementById(keyItem.id).style.backgroundColor = color
			}, 90)

			this.onKeyPadClick(keyItem.id, keyItem.class, keyItem.icon)
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
        		<Screen onKeyUp={this.onKeyUp} screenString={this.state.screenString} />
				
				<div className="Keypad">
                	{this.digitDiv}
            	</div>
      		</div>
    	)
  	}
}

export default App;

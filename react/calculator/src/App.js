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

	digitDiv = digit.map((item) => {
        return (
			<Keypad id={item.id} key={item.id} class={item.class} icon={item.icon} onclick={() => {return this.onKeyPadClick(item.id, item.class, item.icon)} } />
        )
	})

	eval = (items, op) => {
		return items.reduce((ans, item, pos) => {
			if (op == '+') {
				return ans + parseFloat(item)
			} else if (op == '-') {
				return pos === 0 ? parseFloat(item) : (ans - parseFloat(item))
			} else if (op == '*') {
				return pos === 0 ? parseFloat(item) : (ans * parseFloat(item))
			} else if (op == '/') {
				return pos === 0 ? parseFloat(item) : (ans / parseFloat(item))
			}
		}, 0.0)
	}
	
	evaluate = (expr, op = ['+', '-', '*', '/'], index = 0) => {
		if (index == 4) {
			return expr
		} else {
			let exprParts = expr.split(op[index])
			
			let afterexprParts = exprParts.map((item, pos) => {
				return this.evaluate(item, op, index+1)
			})

			// console.log(afterexprParts, op[index])

			return this.eval(afterexprParts, op[index])
		}
	}

	onKeyPadClick = (id, classname, icon) => {
		// console.log("hello")
		let allClasses = classname.split(' ')

		if (allClasses.indexOf("digit") >= 0) {
			
			if (allClasses.indexOf("decimal") >= 0) {
				let lastSegment = this.state.screenString.split(/[*+/-]+/)
				if (lastSegment[lastSegment.length - 1].indexOf(".") < 0) {
					this.setState((prevState, prevProps) => {
						return {screenString: prevState.screenString === "0" ? icon : prevState.screenString + icon}
					})
				}
			} else {
				this.setState((prevState, prevProps) => {
					return {screenString: prevState.screenString === "0" ? icon : prevState.screenString + icon}
				})
			}

		} else if (allClasses.indexOf("final") >= 0) {

			if (id == "delete") {
				this.setState((prevState, prevProps) => {
					return {screenString: prevState.screenString.slice(0, prevState.screenString.length-1)}
				})
			} else if (id == "clear") {
				this.setState((prevState, prevProps) => {
					return {screenString: "0"}
				})
			} else if (id == "evaluate") {
				this.setState((prevState, prevProps) => {
					return {screenString: this.evaluate(prevState.screenString).toString()}
				})
			} else {

			}

		} else {

			let Segment = this.state.screenString.split(/[*+/-]+/)
			let lastSegment = Segment[Segment.length - 1]

			if (lastSegment === "" || lastSegment === " " || lastSegment === ".") {

			} else {
				this.setState((prevState, prevProps) => {
					return {screenString: prevState.screenString + icon}
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
	
	componentDidMount() {
		document.addEventListener("keyup", this.onKeyUp)
	}

	componentWillUnmount() {
		document.removeEventListener("keyup", this.onKeyUp)
	}

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

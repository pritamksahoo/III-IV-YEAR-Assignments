import React, {Component} from 'react';
import squareCss from './Square.module.css';

export class Square extends Component {
    constructor(props) {
		super(props)
		this.state = {
            curMove: null,
            curState: null
		}
	}

	static getDerivedStateFromProps(props, state) {

		return {
            curMove: props.curMove,
            id: props.id,
            key: props.key,
            curState: props.gameState === 'new' ? null : state.curState
        }
    }
    
    shouldComponentUpdate(nextProps, nextState) {

        let curs = {...this.state}
		curs.curState = null

		let nexts = {...nextState}
		nexts.curState = null

        if (this.state.curState === null && this.state.id === nextProps.curId) {
            return true
        } else if (nextProps.gameState === 'new') {
            return true
        } else if (curs === nexts) {
            return false
        } else if (nextState.curState === this.state.curState) {
            return false
        } else {
            return false
        }
    }
    
    hasAlreadyClicked = () => {
        if (this.state.curState === null) {
            this.props.onClickAction(this.state.id)
        } else {
            
        }
    }

	render() {
        // console.log("hello")
		return (
            <div ref={(elem) => this.comp = elem} className={squareCss.square} id={this.state.id} key={this.state.key}>
                {this.state.curMove !== null ? this.state.curMove : ''}
            </div>
		)
	}

	componentDidMount() {
        this.comp.addEventListener("click", this.hasAlreadyClicked)
	}

	componentDidUpdate() {
        this.state.curState = this.state.curMove
        this.props.updateGrid(this.state.id, this.state.curState)
	}

	componentWillUnmount() {
		this.comp.removeEventListener("click", this.hasAlreadyClicked)
	}
}
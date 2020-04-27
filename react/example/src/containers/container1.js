import React, { Component } from 'react';
import Component1 from '../functional/component1';

import { connect } from 'react-redux';

import * as actions from '../store/actions/actions';
import * as actionTypes from '../store/actions/actionTypes';

class Container1 extends Component {
    render() {
        return (
            <div>
                <button onClick={() => console.log(this.props.prop1)}>Get State</button>
                <button onClick={() => this.props.actionSuccess()}>Dispatch Action 1</button>
                <button onClick={() => this.props.actionFailure()}>Dispatch Action 2</button>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        prop1: state.prop1
    }
}

function mapDispatchToProps(dispatch) {
    return {
        actionSuccess : () => {
            dispatch(actions.success)
        },
        actionFailure: () => {
            dispatch(actions.failure)
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Container1);
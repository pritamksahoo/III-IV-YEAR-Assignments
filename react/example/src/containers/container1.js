import React, { Component } from 'react';
import Component1 from '../functional/component1';

import { connect } from 'react-redux';

import * as actions from '../store/actions/actions';
import * as actionTypes from '../store/actions/actionTypes';

class Container1 extends Component {
    handleSubmit = (event) => {
        event.preventDefault()
        let input = event.target.username.value
        this.props.actionUserInput(input)
    }

    render() {
        return (
            <div>
                <button onClick={() => this.props.auth.login()}>Log In</button>&nbsp;
                <button onClick={() => console.log(this.props)}>Get State</button>
                <form onSubmit={this.handleSubmit}>
                    <input type="text" id="username" />
                    <button id="submit">Submit & Store</button>
                </form>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        prop1: state.Reducer1.prop1,
        username: state.Reducer2.username,
        authenticated: state.AuthReducer.isAuthenticated
    }
}

function mapDispatchToProps(dispatch) {
    return {
        actionSuccess : () => {
            dispatch(actions.success)
        },
        actionFailure: () => {
            dispatch(actions.failure)
        },
        actionUserInput: (input) => {
            dispatch(actions.userInput(input))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Container1);
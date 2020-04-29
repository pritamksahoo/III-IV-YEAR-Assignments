import React, { Component } from 'react';
import { Route, Router, Switch } from 'react-router';

import Component1 from '../functional/component1';
import Header from '../functional/header';
import Container1 from '../containers/container1';
import Callback from '../functional/callback';

import history from '../utils/history';
import Auth from '../utils/auth';
import AuthCheck from '../utils/authCheck';

const auth = new Auth();

const handeleAuth = (props) => {
    if (props.location.hash) {
        auth.handleAuthentication()
    }
}

class Routes extends Component {
    render() {
        return (
            <div>
                <Router history={history}>
                    <div>
                        <Header />
                        <Switch>
                            <Route exact path="/" render={() => <Container1 auth={auth} /> } />
                            <Route path="/callback" render={(props) => { handeleAuth(props); return (<Callback />) }} />
                            <Route path="/authcheck" render={() => <AuthCheck auth={auth} />} />
                            <Route path="/component/:id" component={Component1} />
                        </Switch>
                    </div>
                </Router>
            </div>
        )
    }
}

export {Routes};
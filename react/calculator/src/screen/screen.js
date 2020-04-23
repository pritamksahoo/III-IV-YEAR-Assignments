import React, {Component} from 'react';
import screenClasses from './Screen.module.css';

class Screen extends Component {

    render = () => {
        return (
            <div className={screenClasses.Screen}>
                <textarea name="screenString" id="screenString" rows="1" className={screenClasses.stringArea} value={this.props.screenString} onKeyUp={this.props.onKeyUp} readOnly>
                </textarea>
            </div>
        )
    }
}

export {Screen};
import history from '../utils/history';


const RootRedirect = (props) => {
    // console.log(props)
    if (props.isAuthenticated === true) {
        history.replace("/boards/")
    } else {
        history.replace("/account/")
    }

    return null
}

export default RootRedirect;

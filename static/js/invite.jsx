function Invite(props) {
    const [participants, setParticipants] = React.useState([]);
    const [loggedIn, setLoggedIn] = React.useState(false);
    const [errorMessage, setErrorMessage] = React.useState(null);


    React.useEffect(() => {
        const interval = setInterval(() => {
            $.get('/yelphelper-session-participants.json', (res) => {
                setParticipants(res.participants);
                if (res.logged_in) {
                setLoggedIn(true);
                };
            });
        }, 1000);
        return () => clearInterval(interval);
    },[]);

    function onSuccess() {
        pass
    }

    return (
        <React.Fragment>
            {errorMessage ? <ErrorMessage errorMessage={errorMessage} /> : null}
            {loggedIn ? <ParticipantList participants={participants} /> : null}
            {!loggedIn ? <NewUserForm setErrorMessage={setErrorMessage} onSuccess={onSuccess} /> : null}
            {!loggedIn ? <LoginForm setErrorMessage={setErrorMessage} onSuccess={onSuccess} /> : null}
        </React.Fragment>
    );
}

function ParticipantList(props) {
    const participants = props.participants;
    const participantsInfo = [];
    for (const participant of participants) {
        participantsInfo.push(
            <p>{participant.fname}</p>
        );
    }
    return (
        <div>
            {participantsInfo}
        </div>
    );
    
}

ReactDOM.render(
    <Invite />,
    document.querySelector('#root')
);
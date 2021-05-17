function ResultsContainer(props) {
    const [businessesResults, setBusinessesResults] = React.useState([]);
    const [usersLocations, setUsersLocations] = React.useState([]);
    const businessesInfo = [];

    React.useEffect(() => {
		$.get('/results.json', (result) => {
			setBusinessesResults(result.total_scores);
		});
        $.get('/get-users-locations.json', (result) => {
            setUsersLocations(result.users_locations);
        });
	},[]);

    for (const business of businessesResults) {
        businessesInfo.push(
            <div className="business" key={business.alias}>
                <Business business={business}/>
                <p>{business.total_score}</p>
            </div>
        );
    }

    return (
        <React.Fragment>
            <a href={'/'}>Return to Homepage</a>
            <GoogleMap businesses = {businessesResults} usersLocations = {usersLocations}/>
            <div>{businessesInfo}</div>
        </React.Fragment>
    )
}

ReactDOM.render(
    <ResultsContainer />,
    document.querySelector('#root')
);


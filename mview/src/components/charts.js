import React, {useCallback, useEffect, useState, useRef} from 'react';
import Chart from 'react-apexcharts';

var baseUrl = 'http://127.0.0.1:8000/market/';

const useLoadSymbolForm = (callback) => {
    const [inputSymbol, setInputSymbol] = useState('');

    const handleSubmit = (event) => {
        if(event)
            event.preventDefault();

        callback();
    }

    const handleInputSymbolChange = (event) => {
        event.persist();

        setInputSymbol(event.target.value)
    }

    return {
        handleSubmit,
        handleInputSymbolChange,
        inputSymbol
    };
}

const LoadSymbol = ({setSeries, setInputSymbolLoaded}) => {
    const [submitted, setSubmitted] = useState(false);
    const [requiredFormat, setRequiredFormat] = useState([]);
    const [symbolUrl, setSymbolUrl] = useState('')
    
    const loadData = () => {
        setSubmitted(true);
        setSymbolUrl(baseUrl + inputSymbol + '/')
        setRequiredFormat([]);
    }

    const {handleSubmit, handleInputSymbolChange, inputSymbol} = useLoadSymbolForm(loadData);

    useEffect(() => {
        const getHistoricalData = async () => {
            try {
                const response = await fetch(symbolUrl);
                const historicalData = await response.json();

                var requiredFormatTemp = [];

                for(var timestamp in historicalData.Open) {
                    var dateFormat = new Date(parseInt(timestamp));

                    requiredFormatTemp.push({
                                                x: dateFormat, 
                                                y: [
                                                        historicalData.Open[timestamp.toString()], 
                                                        historicalData.High[timestamp.toString()], 
                                                        historicalData.Low[timestamp.toString()], 
                                                        historicalData.Close[timestamp.toString()]
                                                ]
                                            });
                }

                setRequiredFormat(requiredFormatTemp);
            } catch(error) {
                console.log(error);
            }

            if(requiredFormat.length > 0) {
                const series = [{
                    data: requiredFormat
                }];
        
                setSeries(series);
                setInputSymbolLoaded(true);

                setSubmitted(false);
            }
        };

        if(submitted) {
            getHistoricalData();
        }

    }, [submitted, symbolUrl, requiredFormat]);

    return (
        <div>
            <form>
                <label>Security</label>
                <input 
                    type="text" 
                    name="inputSymbol"
                    value={inputSymbol}
                    onChange={handleInputSymbolChange}
                />

                <button onClick={handleSubmit}>GO</button>
            </form>
        </div>
    )
}

const PriceChart = ({series, step1Loaded, step1Dates, step2Loaded, step2Angle}) => {
    const chartElement = useRef();
    const [options, setOptions] = useState({
        chart: {
            id: 'chart',
            events: {
                dataPointSelection: function(event, charContext, config) {
                    console.log(series[0]['data'][config['selectedDataPoints'][0][0]]['x']);
                    console.log('1')
                }
            }
        },

        width: '650',
        xaxis: {
            type: 'datetime'
        }
    });

    useEffect(() => {
        if(step1Loaded) {            
            console.log(step1Dates[0][0]);
            var xaxis = [];

            

            for(var dateAngle in step1Dates) {
                for(var date in step1Dates[dateAngle]) {
                    xaxis.push({
                        x: new Date(step1Dates[dateAngle][date]).getTime(),
                        label: {
                            text: '[' + dateAngle + ', ' + step1Dates[dateAngle][date] + ']'
                        }
                    })
                }
            }

            var newOptions = {
                chart: {
                    id: 'chart',
                    events: {
                        dataPointSelection: function(event, charContext, config) {
                            console.log(series[0]['data'][config['selectedDataPoints'][0][0]]['x']);
                            console.log('2')
                        }
                    }
                },
        
                width: '650',
                xaxis: {
                    type: 'datetime'
                },
                annotations: {
                    xaxis: xaxis
                }
            }

            setOptions(newOptions);
        }
    }, [step1Loaded])

    useEffect(() => {
        if(step2Loaded) {
            var xaxis = [];

            var firstPivot = {
                x: new Date(step1Dates[0][0]).getTime(),
                label: {
                    text: '[FIRST PIVOT]'
                }
            }

            
            xaxis.push(firstPivot);

            for(var date in step1Dates[step2Angle]) {
                xaxis.push({
                    x: new Date(step1Dates[step2Angle][date]).getTime(),
                    label: {
                        text: '[' + step2Angle + ', ' + step1Dates[step2Angle][date] + ']'
                    }
                })
            }

            var newOptions = {
                chart: {
                    id: 'chart',
                    events: {
                        dataPointSelection: function(event, charContext, config) {
                            console.log(series[0]['data'][config['selectedDataPoints'][0][0]]['x']);
                            console.log('2')
                        }
                    }
                },
        
                width: '650',
                xaxis: {
                    type: 'datetime'
                },
                annotations: {
                    xaxis: xaxis
                }
            }

            setOptions(newOptions);
        }
    }, [step2Loaded])

    return (
        <div>
            <div id="newChart">
            </div>
            <Chart
                ref = {chartElement} 
                id = "mainChart"
                options = {options}
                series = {series}
                type = "candlestick"
            />
        </div>
    )
}

const GannDateForecast = ({setStep1Loaded, setStep1Dates, setStep2Loaded, setStep2Angle}) => {
    const [inputs, setInputs] = useState({
        pivot1: '',
        pivot2: ''
    });

    const [pivot1Submit, setPivot1Submit] = useState(false);
    const [pivot2Submit, setPivot2Submit] = useState(false);

    const handleInputChange = (event) => {
        event.persist();

        setInputs(inputs => ({
            ...inputs,
            [event.target.name]: event.target.value
        }));
    }

    const handlePivot1Submit = (event) => {
        if(event)
            event.preventDefault();

        setPivot1Submit(true);
        setStep1Loaded(false);
        setStep1Dates({});
    }

    const handlePivot2Submit = (event) => {
        if(event)
            event.preventDefault();

        setPivot2Submit(true);
        setStep2Loaded(false);
        setStep2Angle('');
    }

    useEffect(() => {
        const updateStep2Angle = async () => {
            setStep2Loaded(true);  
            setStep2Angle(inputs.pivot2);
            setPivot2Submit(false);
        }

        if(pivot2Submit)
            updateStep2Angle();
    }, [pivot2Submit]);

    useEffect(() => {
        const getGannDates = async () => {
            try {
                const response = await fetch(baseUrl + 'gann/1/' + inputs.pivot1 + '/');
                const data = await response.json()

                for(var dateAngle in data) {
                    if(dateAngle != 0)
                        data[dateAngle].splice(0, 1);
                }

                setStep1Loaded(true);  
                setStep1Dates(data);
                setPivot1Submit(false);
            } catch(error) {
                console.log(error);
            }
        }

        if(pivot1Submit)
            getGannDates();
    }, [pivot1Submit]);

    return (
        <div>
            <label>Pivot 1 DATE </label>
            <input 
                name="pivot1" 
                type="text"
                value={inputs.pivot1}
                onChange={handleInputChange}
            />

            <button onClick={handlePivot1Submit}>SUBMIT PIVOT 1</button>

            <label>Pivot 2 ANGLE </label>
            <input 
                name="pivot2" 
                type="text"
                value={inputs.pivot2}
                onChange={handleInputChange}
            />

            <button onClick={handlePivot2Submit}>SUBMIT PIVOT 2</button>
        </div>
    )
}

const MyCharts = () => {
    var [series, setSeries] = useState([]);
    var [inputSymbolLoaded, setInputSymbolLoaded] = useState(false);
    
    var [step1Loaded, setStep1Loaded] = useState(false);
    var [step1Dates, setStep1Dates] = useState({});
    
    var [step2Loaded, setStep2Loaded] = useState(false);
    var [step2Angle, setStep2Angle] = useState('');
   
    return (
        <div>
            <LoadSymbol
                setSeries = {setSeries}
                setInputSymbolLoaded = {setInputSymbolLoaded}
            />

            {
                inputSymbolLoaded &&
                <PriceChart
                    series = {series}
                    step1Loaded = {step1Loaded}
                    step1Dates = {step1Dates}
                    step2Loaded = {step2Loaded}
                    step2Angle = {step2Angle}
                />
            }

            <GannDateForecast
                setStep1Loaded = {setStep1Loaded}
                setStep1Dates = {setStep1Dates}
                setStep2Loaded = {setStep2Loaded}
                setStep2Angle = {setStep2Angle}
            />
        </div>
    )
}

export default MyCharts
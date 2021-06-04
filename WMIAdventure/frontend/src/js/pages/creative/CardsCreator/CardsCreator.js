import React from 'react';

import Main from './styled-components/Main';
import Wrapper from './styled-components/Wrapper';
import Form from './styled-components/Form';
import Div from './styled-components/Div';
import Button from './styled-components/Button';

import CardDescribePreview from './atoms/CardDescribePreview';
import CardDescribeInputs from './atoms/CardDescribeInputs';
import CardProperties from './organisms/CardProperties';
import NavHeader from '../global/molecules/NavHeader';
import CardChoose from './molecules/CardChoose';

class CardsCreator extends React.Component {
    state = {
        cardName: 'Nazwa Karty',
        cardSubject: 'Przedmiot',
        cardTooltip: 'Opis Karty',
        levelCostValues: [],
        effectsFromApi: [],
        effectsToSend: [[], [], []],
        showDescribeInputs: false,

        headerLabel: '',
        showCardChoose: false,
        cardsFromApi: [],
        levelsList: [],
    }

    sendCardToApi = (event) => {
        event.preventDefault();

        const levelsToSend = [];
        for(let i=0; i < this.state.effectsToSend.length; i++) {
            if(this.state.effectsToSend[i].length !== 0) {
                levelsToSend.push (
                    {
                        level: String(i + 1),
                        next_level_cost: this.state.levelCostValues[i],
                        effects: this.state.effectsToSend[i]
                    }
                );
            }
        }

        const API = process.env['REACT_APP_API_URL'];
        try {
            let result = fetch(`http://${API}/api/cards/`, {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({
                    name: this.state.cardName,
                    subject: this.state.cardSubject,
                    image: null,
                    tooltip: this.state.cardTooltip,
                    levels: levelsToSend
                })
            });

            console.log('Result: ' + result);
        } catch (e) {
            console.log(e);
        }
    }

    componentDidMount() {
        if(this.props.creatorType === 'edit')
            this.setState({headerLabel: 'Edytowanie karty', showCardChoose: true});
        else if(this.props.creatorType === 'create')
            this.setState({headerLabel: 'Nowa karta', showCardChoose: false});

        const API = process.env['REACT_APP_API_URL'];

        if(this.props.creatorType === 'edit') {
            fetch(`http://${API}/api/cards/`)
                .then(response => {
                    return response.json();
                })
                .then(data => this.setState({cardsFromApi: data}))
                .catch(error => console.log(error));
        }

        fetch(`http://${API}/api/cards/card-effect/`)
            .then(response => {
                return response.json();
            })
            .then(data => this.setState({effectsFromApi: data}))
            .catch(error => console.log(error));
    }

    showDescribeInputsHandler = (event) => {
        event.preventDefault();
        this.setState({showDescribeInputs: true});
    }

    hideDescribeInputsHandler = (event) => {
        event.preventDefault();
        this.setState({showDescribeInputs: false});
    }

    updateDescribePreview = (event) => {
        const keyName = event.target.name;
        let keyValue;
        if(event.target.value !== '')
            keyValue = event.target.value;
        else keyValue = '-';
        this.setState({[keyName]: keyValue});
    }

    levelCostValuesHandler = (event) => {
        let newList = this.state.levelCostValues.slice();
        if(event.target.value > 0)
            newList[Number(event.target.id[0]) - 1] = event.target.value;
        else newList[Number(event.target.id[0]) - 1] = undefined;
        this.setState({levelCostValues: newList});
    }

    levelCostClearHandler = (event, rank) => {
        event.preventDefault();
        let newList = this.state.levelCostValues.slice();
        newList[rank - 1] = undefined;
        this.setState({levelCostValues: newList});
    }

    levelCostResetHandler = (event, rank) => {
        event.preventDefault();
        let newList = this.state.levelCostValues.slice();
        newList[rank - 1] = 1;
        this.setState({levelCostValues: newList});
    }

    setEffectsToSendHandler = (effects) => {
        this.setState({effectsToSend: effects});
    }

    hideCardChooseHandler = (event) => {
        event.preventDefault();
        this.setState({showCardChoose: false});
    }

    chosenCardHandler = (event, name, subject, tooltip, levels) => {
        event.preventDefault();
        this.setState({
            cardName: name,
            cardSubject: subject,
            cardTooltip: tooltip
        });

        console.log(levels);
        this.setLevelsList(levels);
        this.setLevelCostValues(levels);
        this.hideCardChooseHandler(event);
    }

    setLevelsList = (levels) => {
        let newLevelsList = [];
        for (let i=0; i<levels.length; i++) {
            newLevelsList.push(levels[i].level);
        }
        this.setState({levelsList: newLevelsList});
    }

    setLevelCostValues = (levels) => {
        let newCostList = this.state.levelCostValues.slice();
        try {
            if(levels[0].next_level_cost)
                newCostList[levels[0].level - 1] = levels[0].next_level_cost;
            if(levels[1].next_level_cost)
                newCostList[levels[1].level - 1] = levels[1].next_level_cost;
            this.setState({levelCostValues: newCostList});
        } catch (error) {
            console.log(error);
        }
    }

    render() {
        return (
            <>
                <CardChoose showCardChoose={this.state.showCardChoose}
                            hideCardChooseHandler={this.hideCardChooseHandler}
                            cardsFromAPI={this.state.cardsFromApi}
                            chosenCardHandler={this.chosenCardHandler} />
                <Wrapper>
                    <NavHeader backLink={'/cards-creator-start'} label={this.state.headerLabel} />
                    <Main>
                        <CardDescribePreview cardName={this.state.cardName}
                            cardSubject={this.state.cardSubject}
                            cardTooltip={this.state.cardTooltip}
                            showDescribeInputsHandler={this.showDescribeInputsHandler}
                        />
                        <Form>
                            <CardDescribeInputs updateDescribePreview={this.updateDescribePreview}
                                show={this.state.showDescribeInputs}
                                hideDescribeInputsHandler={this.hideDescribeInputsHandler}
                            />
                            <CardProperties creatorType={this.props.creatorType}
                                levelCostValues={this.state.levelCostValues}
                                levelCostValuesHandler={this.levelCostValuesHandler}
                                levelCostClearHandler={this.levelCostClearHandler}
                                levelCostResetHandler={this.levelCostResetHandler}
                                effectsFromApi={this.state.effectsFromApi}
                                setEffectsToSendHandler={this.setEffectsToSendHandler}
                                levelsList={this.state.levelsList}
                            />
                            <Div>
                                <Button type='submit' onClick={this.sendCardToApi}>
                                    Wyślij
                                </Button>
                            </Div>
                        </Form>
                    </Main>
                </Wrapper>
            </>
        );
    }
}

export default CardsCreator;
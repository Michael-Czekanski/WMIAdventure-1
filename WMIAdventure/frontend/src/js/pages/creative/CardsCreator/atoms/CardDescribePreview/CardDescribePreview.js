import React from 'react';
import H1 from './styled-components/H1';
import P from './styled-components/P';
import Section from './styled-components/Section';
import Pencil from "./styled-components/Pencil";
import Container from "./styled-components/Container";
import Button from "./styled-components/Button"

class CardDescribePreview extends React.Component {
    render() {
        return (
            <Container>
                {/* Button which is positioned over whole container so that the content is clickable */}
                <Button onClick={this.props.showDescribeInputsHandler}>
                </Button>

                {/* Pencil icon */}
                <Pencil>
                </Pencil>

                {/* Main content section */}
                <Section>
                    <H1>
                        {this.props.cardName ? this.props.cardName : 'Nazwa karty'}
                    </H1>
                    <P>
                        {this.props.cardSubject ? this.props.cardSubject : 'Przedmiot'}
                    </P>
                    <P tooltip>
                        {this.props.cardTooltip ? this.props.cardTooltip : 'Opis Karty'}
                    </P>
                </Section>

                {/* Invisible pencil used to center main section in container flexbox */}
                <Pencil invisible={true}>
                </Pencil>
            </Container>
        );
    }
}

export default CardDescribePreview;
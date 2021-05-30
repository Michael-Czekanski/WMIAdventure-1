import styled from 'styled-components';
import Div from './Div';

function showHandler(existNextCardRank, activateCardRank) {
    if(existNextCardRank && activateCardRank === 1)
        return 'flex';
    return 'none';
}

const CommonDiv = styled(Div)`
  display: ${({existNextCardRank, activateCardRank}) => showHandler(existNextCardRank, activateCardRank)};
`;

export default CommonDiv;
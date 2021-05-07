import styled from 'styled-components';
import Image from './Image';

const StyledButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;

  background-color: ${({theme}) => theme.colors.ui01};
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  outline-color: ${({theme}) => theme.colors.brand01};
  padding: 0;
  margin: 0 52px 0 0;
`;

StyledButton.Image = Image;

export default StyledButton;
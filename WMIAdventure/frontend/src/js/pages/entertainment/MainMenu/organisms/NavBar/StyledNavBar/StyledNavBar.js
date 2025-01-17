import styled from 'styled-components';
import IconsWrapper from './IconsWrapper';
import Navigation from './Navigation';

const StyledNavBar = styled.header`
  background-color: ${({theme}) => theme.colors.ui04};
  width: 100%;
  height: 48px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 3;
  
  @media (min-width: 768px) {
    height: 64px;
  }
`;

StyledNavBar.IconsWrapper = IconsWrapper;
StyledNavBar.Navigation = Navigation;

export default StyledNavBar;
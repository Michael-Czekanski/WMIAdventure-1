import styled from 'styled-components';

const Li = styled.li`
  font-size: 18px;
  font-weight: 700;
  text-align: center;
  
  a {
    color: ${({theme}) => theme.colors.ui07};
    text-decoration: none;
  }
`

export default Li;
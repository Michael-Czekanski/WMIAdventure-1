import styled from 'styled-components';

const InputNumber = styled.input`
  margin: 0;
  padding: 0;
  border: none;
  text-align: center;
  width: 28px;
  height: 26px;
  border-bottom: 1px solid ${({theme}) => theme.colors.borderLine};
  -moz-appearance: textfield;

  ::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
`;



export default InputNumber;
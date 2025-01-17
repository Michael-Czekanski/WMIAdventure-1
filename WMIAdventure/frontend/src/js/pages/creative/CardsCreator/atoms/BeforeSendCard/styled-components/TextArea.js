import styled from 'styled-components';

const TextArea = styled.textarea`
  /* Flex options */
  align-self: stretch;
  
  /* textarea options */
  resize: none;
  padding: 12px;
  
  /* Styling */
  border-radius: 4px;
  border: none;
  background-color: ${({theme}) => theme.colors.grey1};
  
  font-size: 18px;
  font-weight: ${({theme}) => theme.weight.light};
  
  :focus {
    outline: dotted 1px ${({theme}) => theme.colors.grey3};
  }
`;

export default TextArea;
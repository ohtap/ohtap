import React from 'react';
import Keyword_Lists from './Collections';
import { mount } from 'enzyme'

it('renders without crashing', () => {
  mount(<Collections />);
});

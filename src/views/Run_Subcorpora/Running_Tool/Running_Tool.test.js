import React from 'react';
import Running_Tool from './Running_Tool';
import { mount } from 'enzyme'

it('renders without crashing', () => {
  mount(<Running_Tool />);
});

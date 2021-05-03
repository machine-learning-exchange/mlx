/* 
*  Copyright 2021 IBM Corporation
* 
*  Licensed under the Apache License, Version 2.0 (the "License"); 
*  you may not use this file except in compliance with the License. 
*  You may obtain a copy of the License at 
* 
*      http://www.apache.org/licenses/LICENSE-2.0 
* 
*  Unless required by applicable law or agreed to in writing, software 
*  distributed under the License is distributed on an "AS IS" BASIS, 
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
*  See the License for the specific language governing permissions and 
*  limitations under the License. 
*/ 
import React, { ReactNode } from 'react';
import styled from 'styled-components'
import Typography from '@material-ui/core/Typography'


interface HeroProps {
  title: string
  subtitle: string
  children?: ReactNode
  alternate?: boolean
}

function Hero(props: HeroProps) {
  const { title, subtitle, alternate, children } = props

  return (
    <Wrapper alternate={alternate}>
      <Typography
        component="h1"
        variant="h2"
        align="center"
        gutterBottom
      >
        {title}
      </Typography>
      <Typography
        className="hero-subtitle"
        variant="h6"
        align="center"
        paragraph
      >
        { subtitle || "Loading..." }
      </Typography>
      <Container>{children}</Container>
    </Wrapper>
  )
}


const backgrounds = [
  'https://s3.us.cloud-object-storage.appdomain.cloud/ibmdev/backgrounds/hero_dark.jpg',
  'https://s3.us.cloud-object-storage.appdomain.cloud/ibmdev/backgrounds/hero_dark.jpg'
]

const Wrapper = styled.div<{ alternate: boolean }>`
  background-image: url(${ ({ alternate: alt }) => alt ? backgrounds[0] : backgrounds[1] });
  background-repeat: no-repeat;
  background-position: center top;
  background-size: cover;
  padding: 2rem 0;

  h1 {
    font-size: 3.5rem;
  }

  h1::first-letter {
    text-transform: capitalize;
  }

  h1, h2, h3, h4, h5, h6 {
    color: #fff;
  }
`

const Container = styled.div`
  display: flex;
  justify-content: center;

  > * {
    margin: 0 8px;
  }
`

export default Hero

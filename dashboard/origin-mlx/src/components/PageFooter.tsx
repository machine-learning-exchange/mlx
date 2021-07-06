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
import React from 'react';
import Link from './Link'

export default function PageFooter() {
    return (
        <h5 className="footer-text"> 
          Copyright © 2021 Machine Learning eXchange The Linux Foundation®. 
          All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. 
          For a list of trademarks of The Linux Foundation, please see our <Link to="https://www.linuxfoundation.org/trademark-usage"> Trademark Usage </Link> 
          page. 
          Linux is a registered trademark of Linus Torvalds. 
          <Link to="https://www.linuxfoundation.org/privacy"> Privacy Policy </Link> 
          and 
          <Link to="https://www.linuxfoundation.org/terms"> Terms of Use </Link>.
        </h5>
    )
}
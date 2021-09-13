/* 
* Copyright 2021 IBM Corporation
* 
* SPDX-License-Identifier: Apache-2.0
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
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
import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import DataListItem from './DataListItem';

export interface IDataListProps {
  title?: string;
  titleIcon?: JSX.Element;
  items: Array<any | React.ReactElement<any>>;
}

export default function DataList (props: IDataListProps) {
    const { title, titleIcon, items } = props;
    return (
      <dl style={{ width: '100%' }}>
        <Typography 
          variant="h5" 
          className="inputs-label">
          { title } { titleIcon }
        </Typography>
        {items.map((item: any, i: number) => {
          return (React.isValidElement(item))
            ? <i key={i}>{item}</i>
            : <DataListItem 
                key={i + item.name} 
                name={item.name} 
                data={item.data} 
                defaultData={item.defaultData}
                options={item.options}
                savedValue={item.savedValue} 
                thirdColData={item.thirdColData}
                itemClass={item.itemClass}
                handleSelect={item.handleSelect}
                handleClick={item.handleClick}
                handleType={item.handleType}
                handleFile={item.handleFile}
                progress={item.progress}
                saveValue={item.saveValue}
              />
          }
          )}
      </dl>
    );
}

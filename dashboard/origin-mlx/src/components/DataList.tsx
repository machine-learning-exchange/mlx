/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
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

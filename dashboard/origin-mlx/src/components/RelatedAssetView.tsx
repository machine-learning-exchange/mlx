/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, {
  useContext, FormEvent, ChangeEvent, useState,
} from 'react';
import TextField from '@material-ui/core/TextField';
import StoreContext from '../lib/stores/context';

import { requestArtifactRun } from '../lib/api/run';
import Button from './Button';

interface RelatedAssetsProps {
  datasetId: string;
  relatedAssets: string[];
  setRunLink?: Function;
}

interface NotebookRunParams {
  [name:string]: {
    runname:string,
    dataset_pvc:string,
    mount_path:string
  }
}

function RelatedAssetView(props: RelatedAssetsProps) {
  const { store } = useContext(StoreContext);
  const { api, kfp } = store.settings.endpoints;
  const API = api.value ? api.value : api.default;
  const KFP = kfp.value ? kfp.value : kfp.default;
  const { setRunLink } = props;

  const initRun : NotebookRunParams = {};
  props.relatedAssets.forEach((relatedAsset: string) => {
    initRun[relatedAsset] = {
      runname: '',
      dataset_pvc: '',
      mount_path: '',
    };
  });

  const [run, setRun] = useState(initRun);

  function handleClick(asset: string) {
    const payload = {
      name: run[asset].runname,
      dataset_pvc: run[asset].dataset_pvc,
      mount_path: run[asset].mount_path,
    };
    const typeIdSplit = asset.split('/');

    return ((event: FormEvent<HTMLFormElement>) => {
      requestArtifactRun(API, typeIdSplit[0], typeIdSplit[1], payload)
        .then(({ run_url }) => {
          setRunLink(`${KFP}/pipeline/#${run_url}`);
        });
    });
  }

  return (
    <div className="runview-wrapper">
      <div style={{ width: '98%', height: '100%', paddingRight: '2%' }}>
        <h2>Related Assets</h2>
        { props.relatedAssets.map((relatedAsset: any) => (
          <div key={relatedAsset}>
            <h4>{relatedAsset}</h4>
            <div className="submit-button-wrapper">
              <TextField
                autoCorrect="false"
                    // id='runName'
                    // className="run-name-input"
                label="Run Name"
                    // placeholder={asset.name}
                helperText="Enter a name to be used for the trial run."
                value={run[relatedAsset].runname}
                fullWidth
                margin="normal"
                variant="outlined"
                InputLabelProps={{ shrink: true }}
                style={{ backgroundColor: 'blue !important' }}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, [relatedAsset]: { ...run[relatedAsset], runname: e.currentTarget.value } })}
              />
              <TextField
                key="dataset-pvc"
                label="Dataset PVC"
                helperText="Enter a dataset pvc to be used"
                value={run[relatedAsset].dataset_pvc}
                autoCorrect="false"
                fullWidth
                margin="normal"
                style={{ marginBottom: '2%' }}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, [relatedAsset]: { ...run[relatedAsset], dataset_pvc: e.currentTarget.value } })}
              />
              <TextField
                key="mount-path"
                label="Mount Path"
                helperText="Enter a mount path to be used"
                value={run[relatedAsset].mount_path}
                autoCorrect="false"
                fullWidth
                margin="normal"
                style={{ marginBottom: '2%' }}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, [relatedAsset]: { ...run[relatedAsset], mount_path: e.currentTarget.value } })}
              />
              <Button
                onClick={handleClick(relatedAsset)}
                type="submit"
                className="hero-buttons submit-run-button"
                variant="contained"
                color="primary"
              >
                Launch
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RelatedAssetView;

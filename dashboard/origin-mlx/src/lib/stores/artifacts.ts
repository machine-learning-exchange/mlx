// Copyright 2021 The MLX Contributors
// 
// SPDX-License-Identifier: Apache-2.0
import { withPersistence } from './util'
import { State, Action } from './types'

export interface Artifact {
  type: string
  id: string
  name: string
  description: string
  created_at: string
  featured: boolean | 1 | 0
  publish_approved: boolean | 1 | 0
  parameters: Object[]
  metadata?: Object
  labels?: string[]
  domain?: string
  framework?: string
  trainable?: boolean
  trainable_tested_platforms?: string[]
  servable?: boolean
  servable_tested_platforms?: string[]
  error?: string
}

export interface ArtifactState extends State {
  pipelines: Artifact[]
  datasets: Artifact[]
  components: Artifact[]
  models: Artifact[]
  notebooks: Artifact[]
  inferenceservices: Artifact[]
}

const initial: ArtifactState = {
  pipelines: [],
  datasets: [],
  components: [],
  models: [],
  notebooks: [],
  inferenceservices: []
}

export const UPDATE_ARTIFACT_ASSET = 'UPDATE_ARTIFACT_ASSET'
export const FETCH_ARTIFACT_ASSETS = 'FETCH_ARTIFACT_ASSETS'

export interface FetchArtifactAssetsAction extends Action {
  type: typeof FETCH_ARTIFACT_ASSETS,
  assetType: string
  assets: Artifact[]
}

export interface UpdateArtifactAsset extends Action {
  type: typeof UPDATE_ARTIFACT_ASSET,
  id: string,
  assetType: string
  payload: Partial<Artifact>
}

export type ArtifactAction =
  FetchArtifactAssetsAction | UpdateArtifactAsset

function reducer(state: State, action: Action) {
  if (action as ArtifactAction) {
    switch (action.type) {
      case FETCH_ARTIFACT_ASSETS: {
        const { assetType, assets } = action as FetchArtifactAssetsAction
        // console.log(assets)
        return { ...state, [assetType]: assets }
      }
      case UPDATE_ARTIFACT_ASSET: {
        const { assetType, id, payload } = action as UpdateArtifactAsset
        return { ...state, [assetType]: state[assetType].map((asset: Artifact) => {
          return asset.id !== id ? asset : { ...asset, ...payload }
        })}
      }
      default:
        return state
    }
  }
}

export default withPersistence('artifacts', reducer)
export { initial as ArtifactInitial }

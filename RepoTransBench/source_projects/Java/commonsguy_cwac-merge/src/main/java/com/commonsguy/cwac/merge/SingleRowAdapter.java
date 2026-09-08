/***
  Copyright (c) 2008-2012 CommonsWare, LLC
  Licensed under the Apache License, Version 2.0 (the "License"); you may not
  use this file except in compliance with the License. You may obtain a copy
  of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless required
  by applicable law or agreed to in writing, software distributed under the
  License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
  OF ANY KIND, either express or implied. See the License for the specific
  language governing permissions and limitations under the License.
  
  From _The Busy Coder's Guide to Android Development_
    http://commonsware.com/Android
 */

package com.commonsguy.cwac.merge;

import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;

class SingleRowAdapter extends BaseAdapter {
  private View row=null;
  private boolean enabled=false;

  SingleRowAdapter(View row, boolean enabled) {
    this.row=row;
    this.enabled=enabled;
  }

  @Override
  public int getCount() {
    return(1);
  }

  @Override
  public Object getItem(int position) {
    return(row);
  }

  @Override
  public long getItemId(int position) {
    return(position);
  }

  @Override
  public View getView(int position, View convertView, ViewGroup parent) {
    return(row);
  }

  @Override
  public boolean areAllItemsEnabled() {
    return(enabled);
  }

  @Override
  public boolean isEnabled(int position) {
    return(enabled);
  }
}
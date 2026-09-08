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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import android.database.DataSetObserver;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListAdapter;

/**
 * Adapter that can merge multiple child adapters into a single
 * contiguous whole.
 * <p>
 * This class is NOT thread-safe.
 * <p>
 * For a sample application, see
 * https://github.com/commonsguy/cwac-merge/
 */
public class MergeAdapter extends BaseAdapter {
  protected ArrayList<ListAdapter> pieces=new ArrayList<ListAdapter>();

  /**
   * Varargs version of the constructor.
   * 
   * @param adapters
   *          Zero or more ListAdapters to {@link #addAdapter(ListAdapter)}
   */
  public MergeAdapter(ListAdapter... adapters) {
    this(Arrays.asList(adapters));
  }

  /**
   * Constructor
   * 
   * @param adapters
   *          List of ListAdapters to {@link #addAdapter(ListAdapter)}
   */
  public MergeAdapter(List<ListAdapter> adapters) {
    super();

    for (ListAdapter adapter : adapters) {
      addAdapter(adapter);
    }
  }

  /**
   * Adds a new adapter to the end of the existing list of adapters.
   * 
   * @param adapter
   *          A ListAdapter to be added
   */
  public void addAdapter(ListAdapter adapter) {
    pieces.add(adapter);
    adapter.registerDataSetObserver(new CascadeDataSetObserver());
  }

  /**
   * Adds a new adapter to the end of the existing list of adapters.
   * 
   * @param view
   *          A View to be wrapped in an {@link #addAdapter(ListAdapter)}
   */
  public void addView(View view) {
    addView(view, false);
  }

  /**
   * Adds a new adapter to the end of the existing list of adapters.
   * 
   * @param view
   *          A View to be wrapped in an {@link #addAdapter(ListAdapter)}
   * @param enabled
   *          true if the view is enabled for clicking, false otherwise
   */
  public void addView(View view, boolean enabled) {
    pieces.add(new SingleRowAdapter(view, enabled));
  }

  /**
   * Insert a new adapter in the list of adapters
   * 
   * @param adapter
   *          A ListAdapter to be added
   * @param index
   *          Index for insertion
   */
  public void insertAdapter(ListAdapter adapter, int index) {
    pieces.add(index, adapter);
    adapter.registerDataSetObserver(new CascadeDataSetObserver());
  }

  /**
   * Insert a new adapter in the list of adapters
   * 
   * @param view
   *          A View to be wrapped in an {@link #addAdapter(ListAdapter)}
   * @param index
   *          Index for insertion
   */
  public void insertView(View view, int index) {
    insertView(view, index, false);
  }

  /**
   * Insert a new adapter in the list of adapters
   * 
   * @param view
   *          A View to be wrapped in an {@link #addAdapter(ListAdapter)}
   * @param index
   *          Index for insertion
   * @param enabled
   *          true if the view is enabled for clicking, false otherwise
   */
  public void insertView(View view, int index, boolean enabled) {
    pieces.add(index, new SingleRowAdapter(view, enabled));
  }

  /**
   * Get the data item associated with the specified position in the
   * data set.
   * 
   * @param position
   *          Position of the item whose data we want
   */
  @Override
  public Object getItem(int position) {
    for (ListAdapter piece : pieces) {
      int size = piece.getCount();

      if (position < size) {
        return (piece.getItem(position));
      }

      position -= size;
    }

    return (null);
  }

  /**
   * How many items are in the data set represented by this Adapter.
   */
  @Override
  public int getCount() {
    int total = 0;

    for (ListAdapter piece : pieces) {
      total += piece.getCount();
    }

    return (total);
  }

  /**
   * Get the type of View that will be created by
   * {@link #getView(int, View, ViewGroup)} for the specified item.
   * 
   * @param position
   *          Position of the item whose View type we want
   */
  @Override
  public int getItemViewType(int position) {
    int typeOffset = 0;
    int result = -1;

    for (ListAdapter piece : pieces) {
      int size = piece.getCount();

      if (position < size) {
        result = typeOffset + piece.getItemViewType(position);
        break;
      }

      position -= size;
      typeOffset += piece.getViewTypeCount();
    }

    return (result);
  }

  /**
   * Returns the number of types of Views that will be created by
   * {@link #getView(int, View, ViewGroup)}.
   */
  @Override
  public int getViewTypeCount() {
    int total = 0;

    for (ListAdapter piece : pieces) {
      total += piece.getViewTypeCount();
    }

    return (Math.max(total, 1)); // defensive -- should always be at
                                 // least one
  }

  /**
   * Get the position within the entire data set for the specified
   * row
   * 
   * @param adapter
   *          ListAdapter in which the row lies
   * @param position
   *          Position within the specified adapter
   * @return Overall position of the row
   */
  public int getPosition(ListAdapter adapter, int position) {
    int result = 0;

    for (ListAdapter piece : pieces) {
      if (piece.equals(adapter)) {
        return (result + position);
      }

      result += piece.getCount();
    }

    return (-1);
  }

  /**
   * Get a View that displays the data at the specified position in
   * the data set.
   * 
   * @param position
   *          Position of the item whose View we want
   * @param convertView
   *          View to recycle, if not null
   * @param parent
   *          ViewGroup containing the returned View
   */
  @Override
  public View getView(int position, View convertView, ViewGroup parent) {
    for (ListAdapter piece : pieces) {
      int size = piece.getCount();

      if (position < size) {
        return (piece.getView(position, convertView, parent));
      }

      position -= size;
    }

    return (null);
  }

  /**
   * Are all items in this Adapter enabled? If so, it means that all
   * items are selectable and clickable.
   */
  @Override
  public boolean areAllItemsEnabled() {
    for (ListAdapter piece : pieces) {
      if (!piece.areAllItemsEnabled()) {
        return (false);
      }
    }

    return (true);
  }

  /**
   * Returns true if the item at the specified position is not a
   * separator. (A separator is a non-clickable item).
   * 
   * @param position
   *          Position of the item whose enabled status we want
   */
  @Override
  public boolean isEnabled(int position) {
    for (ListAdapter piece : pieces) {
      int size = piece.getCount();

      if (position < size) {
        return (piece.isEnabled(position));
      }

      position -= size;
    }

    return (false); // should not happen, but defensive in case
  }

  /**
   * Get the row id associated with the specified position in the
   * list.
   * 
   * @param position
   *          Position of the item whose row ID we want
   */
  @Override
  public long getItemId(int position) {
    for (ListAdapter piece : pieces) {
      int size = piece.getCount();

      if (position < size) {
        return (piece.getItemId(position));
      }

      position -= size;
    }

    return (-1); // should not happen, but defensive in case
  }

  private class CascadeDataSetObserver extends DataSetObserver {
    @Override
    public void onChanged() {
      notifyDataSetChanged();
    }

    @Override
    public void onInvalidated() {
      notifyDataSetInvalidated();
    }
  }
}
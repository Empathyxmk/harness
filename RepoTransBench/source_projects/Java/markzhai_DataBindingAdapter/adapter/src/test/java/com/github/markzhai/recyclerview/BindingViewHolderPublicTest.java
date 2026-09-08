package com.github.markzhai.recyclerview;

import android.databinding.ViewDataBinding;
import android.view.View;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class BindingViewHolderPublicTest {

    private ViewDataBinding binding;
    private View view;

    @Before
    public void setUp() {
        view = Mockito.mock(View.class);
        binding = Mockito.mock(ViewDataBinding.class);
        Mockito.when(binding.getRoot()).thenReturn(view);
    }

    @Test
    public void testGetBindingPublic() {
        BindingViewHolder<ViewDataBinding> holder = new BindingViewHolder<>(binding);
        assertSame(binding, holder.getBinding());
    }
}
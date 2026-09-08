package com.myshop;

import com.myshop.common.event.EventStoreHandler;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static org.hamcrest.Matchers.instanceOf;
import static org.hamcrest.Matchers.notNullValue;
import static org.junit.Assert.assertThat;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(ShopApplication.class)
public class SpringConfigPublicTest {
    @Autowired
    private ApplicationContext applicationContext;

    @Test
    public void eventStoreHandler_bean_has_applicationContext_and_type() throws Exception {
        // Instead of checking the same bean as the original, let's additionally check the total beans of type EventStoreHandler > 0.
        String[] beans = applicationContext.getBeanNamesForType(EventStoreHandler.class);
        assertThat(beans.length, org.hamcrest.Matchers.greaterThan(0));
        for (String beanName : beans) {
            Object bean = applicationContext.getBean(beanName);
            assertThat(bean, notNullValue());
            assertThat(bean, instanceOf(EventStoreHandler.class));
        }
    }
}
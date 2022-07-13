package com.macro.mall.tiny.controller;

import com.macro.mall.tiny.common.api.CommonPage;
import com.macro.mall.tiny.common.api.CommonResult;
import com.macro.mall.tiny.mbg.model.PmsBrand;
import com.macro.mall.tiny.mbg.model.PmsBrandExample;
import com.macro.mall.tiny.service.PmsBrandService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.List;

/**
 * brand管理Controller
 * Created by macro on 2019/4/19.
 */
@Api(tags = "PmsBrandController")
@CrossOrigin(origins = "*", maxAge = 3600)
@Controller
@RequestMapping("/brand")
public class PmsBrandController {
    @Autowired
    private PmsBrandService brandService;

    private static final Logger LOGGER = LoggerFactory.getLogger(PmsBrandController.class);

    @ApiOperation("获取brand列表")
    @RequestMapping(value = "listAll", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<List<PmsBrand>> getBrandList() {
        return CommonResult.success(brandService.listAllBrand());
    }

    @ApiOperation("添加brand")
    @RequestMapping(value = "/create", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult createBrand(@RequestBody PmsBrand pmsBrand) {
        CommonResult commonResult;
        int count = brandService.createBrand(pmsBrand);
        if (count == 1) {
            commonResult = CommonResult.success(pmsBrand);
            LOGGER.debug("createBrand success:{}", pmsBrand);
        } else {
            commonResult = CommonResult.failed("操作失败");
            LOGGER.debug("createBrand failed:{}", pmsBrand);
        }
        return commonResult;
    }

    @ApiOperation("更新指定id的brand信息")
    @RequestMapping(value = "/update/{id}", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult updateBrand(@PathVariable("id") Long id, @RequestBody PmsBrand pmsBrandDto,
            BindingResult result) {
        CommonResult commonResult;
        int count = brandService.updateBrand(id, pmsBrandDto);
        if (count == 1) {
            commonResult = CommonResult.success(pmsBrandDto);
            LOGGER.debug("updateBrand success:{}", pmsBrandDto);
        } else {
            commonResult = CommonResult.failed("操作失败");
            LOGGER.debug("updateBrand failed:{}", pmsBrandDto);
        }
        return commonResult;
    }

    @ApiOperation("删除指定id的brand")
    @RequestMapping(value = "/delete/{id}", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult deleteBrand(@PathVariable("id") Long id) {
        int count = brandService.deleteBrand(id);
        if (count == 1) {
            LOGGER.debug("deleteBrand success :id={}", id);
            return CommonResult.success(null);
        } else {
            LOGGER.debug("deleteBrand failed :id={}", id);
            return CommonResult.failed("操作失败");
        }
    }

    @ApiOperation("分页查询brand列表")
    @RequestMapping(value = "/list", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<CommonPage<PmsBrand>> listBrand(
            @RequestParam(value = "pageNum", defaultValue = "1") @ApiParam("页码") Integer pageNum,
            @RequestParam(value = "pageSize", defaultValue = "3") @ApiParam("每页数量") Integer pageSize) {
        List<PmsBrand> brandList = brandService.listBrand(pageNum, pageSize);
        return CommonResult.success(CommonPage.restPage(brandList));
    }

    @ApiOperation("获取指定id的brand详情")
    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<PmsBrand> brand(@PathVariable("id") Long id) {
        return CommonResult.success(brandService.getBrand(id));
    }

    @ApiOperation("根据样例获取brand")
    @RequestMapping(value = "/exp", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult<List<PmsBrand>> getBrandByExample(@RequestBody PmsBrand pmsBrand)
            throws InvocationTargetException, IllegalAccessException, NoSuchMethodException {
        PmsBrandExample pmsBrandExample = new PmsBrandExample();
        PmsBrandExample.Criteria criteria = pmsBrandExample.createCriteria();
        Class pmsBrandClazz = PmsBrand.class;
        Class criteriaClazz = criteria.getClass();
        Method[] methods = pmsBrandClazz.getDeclaredMethods();
        for (Method method : methods) {
            String methodName = method.getName();
            if (methodName.contains("get")) {
                String fieldName = methodName.substring(3);
                Object fieldValue = method.invoke(pmsBrand, null);
                Class valueClazz = method.getReturnType();
                if (fieldValue != null) {
                    Method criteriaMethod = criteriaClazz.getDeclaredMethod("and" + fieldName + "EqualTo", valueClazz);
                    criteriaMethod.invoke(criteria, fieldValue);
                }
            }
        }
        return CommonResult.success(brandService.getBrandByExample(pmsBrandExample));
    }
}
